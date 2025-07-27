SELECT DISTINCT p2.name FROM people p2
JOIN stars s2 ON p2.id = s2.person_id
WHERE s2.movie_id IN (
    SELECT s1.movie_id FROM people p1
    JOIN stars s1 ON p1.id = s1.person_id
    WHERE p1.name = "Kevin Bacon" AND p1.birth = 1958
) AND p2.name != "Kevin Bacon";
