-- 🕵️ Investigation Log: The Fiftyville Duck Theft
-- Objective: Identify the thief, their escape method, and any accomplice involved.

-- Step 1: Verify the crime occurred on July 28, 2024, at Humphrey Street.
SELECT description
FROM crime_scene_reports
WHERE street = 'Humphrey Street'
  AND year = 2024
  AND month = 7
  AND day = 28;

-- Step 2: Search interviews on the same date for any witnesses mentioning the bakery.
SELECT transcript
FROM interviews
WHERE year = 2024
  AND month = 7
  AND day = 28
  AND transcript LIKE '%bakery%';

-- Step 3: Identify cars that exited the bakery parking lot between 10:15 and 10:25 AM.
-- Join with people to find who was behind the wheel.
SELECT p.name, bsl.license_plate, bsl.activity
FROM bakery_security_logs bsl
JOIN people p ON bsl.license_plate = p.license_plate
WHERE bsl.year = 2024
  AND bsl.month = 7
  AND bsl.day = 28
  AND bsl.hour = 10
  AND bsl.minute BETWEEN 15 AND 25
  AND bsl.activity = 'exit';

-- Step 4: Track ATM withdrawals made on Leggett Street on the day of the theft.
-- Identify people withdrawing cash that day.
SELECT p.name, at.transaction_type, at.amount, at.atm_location
FROM atm_transactions at
JOIN bank_accounts ba ON at.account_number = ba.account_number
JOIN people p ON ba.person_id = p.id
WHERE at.atm_location = 'Leggett Street'
  AND at.year = 2024
  AND at.month = 7
  AND at.day = 28
  AND at.transaction_type = 'withdraw';

-- Step 5: Find short calls (under 60 seconds) made by Bruce on the day of the theft.
-- Used to identify any potential accomplices contacted.
SELECT ph.caller, ph.receiver, ph.duration
FROM phone_calls ph
WHERE ph.year = 2024
  AND ph.month = 7
  AND ph.day = 28
  AND ph.duration < 60
  AND ph.caller IN (
      SELECT phone_number FROM people WHERE name = 'Bruce'
  );

-- Step 6: Find the earliest flight out of Fiftyville on July 29, 2024.
-- Likely used by the thief to flee.
SELECT f.id AS flight_id, a1.city AS origin_city, a2.city AS destination_city,
       f.year, f.month, f.day, f.hour, f.minute
FROM flights f
JOIN airports a1 ON f.origin_airport_id = a1.id
JOIN airports a2 ON f.destination_airport_id = a2.id
WHERE f.year = 2024
  AND f.month = 7
  AND f.day = 29
  AND a1.city = 'Fiftyville'
ORDER BY f.hour, f.minute
LIMIT 1;

-- Step 7: List passengers on the earliest flight to find who escaped with Bruce.
-- Used to identify accomplices.
SELECT p.name, pa.seat
FROM passengers pa
JOIN people p ON pa.passport_number = p.passport_number
WHERE pa.flight_id = (
    SELECT f.id
    FROM flights f
    JOIN airports a1 ON f.origin_airport_id = a1.id
    WHERE f.year = 2024
      AND f.month = 7
      AND f.day = 29
      AND a1.city = 'Fiftyville'
    ORDER BY f.hour, f.minute
    LIMIT 1
);

-- Step 8: Get Robin's phone number to cross-reference call records.
SELECT name, phone_number
FROM people
WHERE name = 'Robin';

-- Step 9: Confirm whether Bruce and Robin communicated briefly on the day of the theft.
-- Verifies if Robin was the accomplice Bruce contacted.
SELECT ph.caller, ph.receiver, ph.duration
FROM phone_calls ph
JOIN people p1 ON ph.caller = p1.phone_number
JOIN people p2 ON ph.receiver = p2.phone_number
WHERE ph.year = 2024
  AND ph.month = 7
  AND ph.day = 28
  AND ph.duration < 60
  AND ((p1.name = 'Bruce' AND p2.name = 'Robin') OR (p1.name = 'Robin' AND p2.name = 'Bruce'));

-- Step 10: Confirm the destination city Bruce fled to.
-- Final confirmation of the escape route.
SELECT a2.city AS destination_city
FROM flights f
JOIN passengers pa ON f.id = pa.flight_id
JOIN people p ON pa.passport_number = p.passport_number
JOIN airports a2 ON f.destination_airport_id = a2.id
WHERE p.name = 'Bruce'
  AND f.year = 2024
  AND f.month = 7
  AND f.day = 29;

-- 🕵️ FINAL INVESTIGATION RESULT
-- -----------------------------
-- ✅ THIEF: Bruce
-- 🛫 ESCAPE DESTINATION: New York City (Airport ID: 4) on Flight #36
-- 🧑‍🤝‍🧑 ACCOMPLICE: Robin
-- -----------------------------
