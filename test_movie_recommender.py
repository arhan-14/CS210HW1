import io
import os
import tempfile
from contextlib import redirect_stdout
import movie_recommender as mr

PASS = 0
FAIL = 0


# ---------------- Utility Helpers ---------------- #


def capture_output(func, *args, **kwargs):
    """Capture printed output."""
    buf = io.StringIO()
    with redirect_stdout(buf):
        func(*args, **kwargs)
    return buf.getvalue().strip()


def mark(pass_condition, desc, expected=None, actual=None):
    """Record pass/fail with detailed printout."""
    global PASS, FAIL
    if pass_condition:
        PASS += 1
        print(f"✅ {desc}")
    else:
        FAIL += 1
        print(f"❌ {desc}")
        if expected is not None or actual is not None:
            print(f"   Expected: {expected}")
            print(f"   Actual:   {actual}")


def make_temp_file(content):
    """Create temp file for edge-case tests."""
    t = tempfile.NamedTemporaryFile(mode="w+", delete=False)
    t.write(content)
    t.flush()
    return t.name


# ---------------- Helper Computations ---------------- #


def expected_movie_popularity(ratings, n):
    avg = {m: sum(r for r, _ in v) / len(v) for m, v in ratings.items()}
    return [k for k, _ in sorted(avg.items(), key=lambda x: x[1], reverse=True)[:n]]


def expected_movie_popularity_in_genre(movies, ratings, genre, n):
    scores = {}
    for m, (g, _) in movies.items():
        if g.lower() == genre.lower() and m in ratings:
            vals = [r for r, _ in ratings[m]]
            scores[m] = sum(vals) / len(vals)
    return [m for m, _ in sorted(scores.items(), key=lambda x: x[1], reverse=True)[:n]]


def expected_genre_popularity(movies, ratings, n):
    movie_avg = {m: sum(r for r, _ in lst) / len(lst) for m, lst in ratings.items()}
    totals, counts = {}, {}
    for m, avg in movie_avg.items():
        if m in movies:
            g = movies[m][0]
            totals[g] = totals.get(g, 0) + avg
            counts[g] = counts.get(g, 0) + 1
    genre_avg = {g: totals[g] / counts[g] for g in totals}
    return sorted(genre_avg.items(), key=lambda x: x[1], reverse=True)[:n]


def expected_user_preference(movies, ratings, user_id):
    totals, counts = {}, {}
    for m, lst in ratings.items():
        if m not in movies:
            continue
        vals = [r for r, uid in lst if uid == user_id]
        if vals:
            g = movies[m][0]
            totals[g] = totals.get(g, 0) + sum(vals) / len(vals)
            counts[g] = counts.get(g, 0) + 1
    if not totals:
        return None
    avg = {g: totals[g] / counts[g] for g in totals}
    return max(avg.items(), key=lambda x: x[1])[0]


def expected_recommendations(user_id, movies, ratings, top=3):
    pref = expected_user_preference(movies, ratings, user_id)
    if not pref:
        return [], pref
    rated = {m for m, lst in ratings.items() if any(uid == user_id for _, uid in lst)}
    genre_movies = [m for m, (g, _) in movies.items() if g.lower() == pref.lower()]
    scores = {}
    for m in genre_movies:
        if m not in rated and m in ratings:
            vals = [r for r, _ in ratings[m]]
            scores[m] = sum(vals) / len(vals)
    recs = [
        m for m, _ in sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top]
    ]
    return recs, pref


# ---------------- Feature Coverage (5 pts) ---------------- #


def test_feature_coverage():
    print("\n=== Feature Coverage Tests ===")
    # if not os.path.exists("movies1.txt") or not os.path.exists("ratings1.txt"):
    #     print("❌ movies1.txt or ratings1.txt not found in directory.")
    #     return

    movies = mr.load_movies_file("movies1.txt")
    ratings = mr.load_ratings_file("ratings1.txt")

    # 1. movie_popularity()
    n = 3
    out = capture_output(mr.movie_popularity, ratings, n)
    actual = [
        l.strip() for l in out.splitlines() if l.strip() and not l.startswith("{")
    ][-n:]
    expected = expected_movie_popularity(ratings, n)
    mark(
        actual == expected[: len(actual)],
        "movie_popularity() top 3 order",
        expected,
        actual,
    )

    # 2. movie_popularity_in_genre()
    genre = "Adventure"
    out = capture_output(mr.movie_popularity_in_genre, movies, ratings, genre, 3)
    actual = [l.split(":")[0].strip() for l in out.splitlines() if ":" in l]
    expected = expected_movie_popularity_in_genre(movies, ratings, genre, 3)
    mark(actual == expected, f"movie_popularity_in_genre({genre})", expected, actual)

    # 3. genre_popularity()
    ret = mr.genre_popularity(movies, ratings, 3)
    expected = expected_genre_popularity(movies, ratings, 3)
    mark(ret == expected, "genre_popularity() return value", expected, ret)

    # 4. user_preference()
    user = 6
    ret = mr.user_preference(movies, ratings, user)
    expected = expected_user_preference(movies, ratings, user)
    mark(ret == expected, f"user_preference({user})", expected, ret)

    # 5. recommend_movies()
    recs, pref = expected_recommendations(user, movies, ratings, 3)
    out = capture_output(mr.recommend_movies, user, movies, ratings)
    actual = []
    for l in out.splitlines():
        l = l.strip()
        # skip header lines
        if not l or l.startswith("User") or l.startswith("Top"):
            continue
        if ":" in l:
            actual.append(l.split(":")[0].strip())

    if "No unrated" in out:
        actual = []

    mark(actual == recs, f"recommend_movies({user})", recs, actual)


# ---------------- Edge/Negative Tests (5 pts) ---------------- #


def test_edge_cases():
    print("\n=== Edge & Negative Tests ===")

    # 1. Empty files
    mf, rf = make_temp_file(""), make_temp_file("")
    m, r = mr.load_movies_file(mf), mr.load_ratings_file(rf)
    mark(m == {} and r == {}, "Empty file handling", "{}", f"{m}, {r}")

    # 2. Malformed rows
    movies_bad = "Action|1|Die Hard\nBadRow\nComedy|2|Mask"
    ratings_bad = "Die Hard|5.0|1\nBadLine\nMask|4.0|2"
    mf, rf = make_temp_file(movies_bad), make_temp_file(ratings_bad)
    out1 = capture_output(mr.load_movies_file, mf)
    out2 = capture_output(mr.load_ratings_file, rf)
    cond = "Skipping malformed" in out1 or "Skipping malformed" in out2
    mark(cond, "Malformed rows skipped gracefully")

    # 3. Duplicate ratings
    movies_dup = "Comedy|1|Mask"
    ratings_dup = "Mask|5.0|1\nMask|5.0|1\nMask|4.0|2"
    mf, rf = make_temp_file(movies_dup), make_temp_file(ratings_dup)
    r = mr.load_ratings_file(rf)
    out = capture_output(mr.movie_popularity, r, 1)
    cond = "Mask" in out
    mark(cond, "Duplicate ratings handled", "Mask in output", out)

    # 4. Non-numeric ratings
    movies_badnum = "Action|1|Die Hard"
    ratings_badnum = "Die Hard|awesome|1"
    mf, rf = make_temp_file(movies_badnum), make_temp_file(ratings_badnum)
    out = capture_output(mr.load_ratings_file, rf)
    cond = "Skipping invalid rating" in out or "Skipping invalid" in out
    mark(cond, "Non-numeric rating skipped", "Warning expected", out)

    # 5. Tie behavior
    movies_tie = """Action|1|Die Hard
Comedy|2|Mask
Comedy|3|Ace Ventura
Action|4|Lethal Weapon"""
    ratings_tie = """Die Hard|5.0|1
Mask|5.0|1
Ace Ventura|5.0|1
Lethal Weapon|5.0|1"""
    mf, rf = make_temp_file(movies_tie), make_temp_file(ratings_tie)
    m, r = mr.load_movies_file(mf), mr.load_ratings_file(rf)
    pref = mr.user_preference(m, r, 1)
    mark(
        pref in ("Action", "Comedy"),
        "Tie behavior deterministic",
        "Action/Comedy",
        pref,
    )


# ---------------- Main ---------------- #


def main():
    print("=== Automated Tester: movie_recommender.py ===")
    test_feature_coverage()
    test_edge_cases()

    total = PASS + FAIL
    print("\n=== Test Summary ===")
    print(f"✅ Passed: {PASS}")
    print(f"❌ Failed: {FAIL}")
    if total:
        print(f"📊 Score: {(PASS / total * 10):.2f}/10 pts")


if __name__ == "__main__":
    main()
