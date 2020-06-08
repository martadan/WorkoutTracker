# WorkoutTracker


## Overview
<p>There are already loads of fitness apps, but most do not have the flexibility to track different styles of workouts in the same app.
I decided to build one out myself to allow the flexibility I want without all the extra features I don't need</p>

<p>
Published live at:<br>
https://dm-workout.herokuapp.com/
</p>

<p>
Coach JWT
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkFKOW9HX3R5eHlHcG1Ub1ZVNlRSTiJ9.eyJpc3MiOiJodHRwczovL2Rldi1sNDUyOXU3Mi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVkZTQ1YWIxNTJlODYwMDE5YTViMTQxIiwiYXVkIjoid29ya291dCIsImlhdCI6MTU5MTY1NDI2NywiZXhwIjoxNTkxNjYxNDY2LCJhenAiOiJhYlF0cjlxeFJzdUl6MWdicjlHZlhFUENIYmNnS29GbSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmV4ZXJjaXNlIiwiZGVsZXRlOndvcmtvdXQiLCJnZXQ6ZXhlcmNpc2UiLCJnZXQ6d29ya291dCIsInBhdGNoOmV4ZXJjaXNlIiwicGF0Y2g6d29ya291dCIsInBvc3Q6ZXhlcmNpc2UiLCJwb3N0OndvcmtvdXQiXX0.rbFCbBqFpl3jPAnqwNmXYPR5cUSGIA1NZu8txnJ19mNA2mUl5Py14z-2N_sXS3IkrRT0HLofnDA1ndfG3-R87dM44pOZ6-Jwp9UiGKpo7CZu5ZylykaSAjq8nf2jpKyEO8hmsSnAHi24CuVGNVcipk5N6QBa9v18hQe5xJ7dBvrkbT1xgx3pso0nLmiz9lDlCSlFnJ7isMbLdWaieQiyYM7Z8nAIjYT4f7ckR2OAEBAg9acjFN_H1uIuha2Tdd0uVt1Ed6vMcixEkJN73sh0KQ2TKjrAJWzMa-KDHspRlOA4V286lOEvbuJRsrX-_sij_4BcKXV7A2AAKJdViLs4VA
<br><br>
Athlete JWT<br>
athlete@test.com<br>
athleteTEST!<br>
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkFKOW9HX3R5eHlHcG1Ub1ZVNlRSTiJ9.eyJpc3MiOiJodHRwczovL2Rldi1sNDUyOXU3Mi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVkZTQ3MTQxNTJlODYwMDE5YTViM2NkIiwiYXVkIjoid29ya291dCIsImlhdCI6MTU5MTY1NDIwMCwiZXhwIjoxNTkxNjYxMzk5LCJhenAiOiJhYlF0cjlxeFJzdUl6MWdicjlHZlhFUENIYmNnS29GbSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmV4ZXJjaXNlIiwiZ2V0OndvcmtvdXQiLCJwYXRjaDp3b3Jrb3V0IiwicG9zdDp3b3Jrb3V0Il19.uhVKtMDCn3vvnkUVIWKQutTjdXB5TBXAGMMuM7wk-_zv4jmRYH2rRh4tbrlY0jPkGklmTfLapQBLYcHw1sagCQiMJXY5EQY72uLwToMI8qz-22jLeu1u8E3xtkLrcoX3PWmhIBncpgS5vwPhfyE7ntXlHbEEk6vUHoaVCbbfQkhx8hPV2j3I8LOMx27C3_2i8WWrEsQCe5d2xkfFdllbA3ctePuju1Pk7s81V6IMoldvVc4bUFOH2khBfkxQ0Ov0UbXBlXe1edsKrEzZ9yttDlJ5sxpuOyXygnYUvBGNk2jMyPBBhirVJnBW4KUEljHDQctk7cZRksqALgGWmZTdFA
</p>


## Current state
API is built out.
Uses unit tests on all routes.
Role-based authorization done through Auth0.
No real front-end put together yet


## API
All routes documented below:

### Workout routes:
#### GET /workouts
Returns all workouts
No data needs to be passed in
Returns json:
```json
{
  "workouts": [list of workout objects formatted as json dicts],
  "success": true
}
```
Returns standard `{"success": false}` and error status code on error

#### GET /workouts/<workout_id>
Returns a particular workout
No data needs to be passed in (aside from workout_id in url)
Returns json:
```json
{
  "workout": workout object formatted in json (including exercise list),
  "success": true
}
```
Returns standard `{"success": false}` and error status code on error
(returns 404 if that workout_id does not exist)

#### POST /workouts
Creates a new workout (including list of exercises in the workout)
Automatically assigns the sequentially next workout_id
Requires the following passed in (json):
```json
{
  "name": name for the workout,
  "focus": "upper", "lower", "cardio", "push", "pull", etc.
  "repeat": boolean. Whether this is a one-off, or a workout to repeat later (not currently utilized)
  "exercises": list of exercises (can be None, and then patched later)
    [
      {
        "name": exercise name. Needs to match an existing exercise,
        "sets": int,
        "reps": int,
        "weight": decimal, accurate to 00.0
      },
      {...}
    ]
}
```
Returns very simple json:
```json
{
  "workout_id": int, id of newly-created workout,
  "success": true
}
```
Returns standard `{"success": false}` and error status code on error

#### PATCH /workouts/<workout_id>
Updates an existing workout
Same json data required as POST /workouts route
Same json return on successful update as the POST /workouts route
Returns standard `{"success": false}` and error status code on error
(returns 404 if workout_id not found)

#### DELETE /workouts/<workout_id>
Deletes an existing workout
No json data needs to be passed in
Returns json and status code (200/404):
```json
{
  "success": true/false,
  "workout_id": int, id of workout deleted
}
```

### Exercise routes:
#### GET /exercises
Returns all exercises
No data needs to be passed in
Returns json:
```json
{
  "exercises": [list of exercise objects formatted as json dicts],
  "success": true
}
```
Returns standard `{"success": false}` and error status code on error

#### GET /exercises/<exercise_id>
Returns a particular exercise
No data needs to be passed in (aside from exercise_id in url)
Returns json:
```json
{
  "exercise": exercise object formatted in json (including list of workouts using this exercise),
  "success": true
}
```
Returns standard `{"success": false}` and error status code on error
(returns 404 if that exercise_id does not exist)

#### POST /exercises
Creates a new exercise (but does not attach it to any workouts yet)
Automatically assigns the sequentially next exercise_id
Requires the following passed in (json):
```json
{
  "name": name for the exercise (must be unique),
  "equipment": "barbell", "dumbbell", "kettlebell", "bodyweight", etc.
  "target": "reps", "time" (unit of reps is seconds if target is time)
  "link": string hyperlink to exercise description/video
}
```
Returns very simple json:
```json
{
  "exercise_id": int, id of newly-created exercise,
  "success": true
}
```
Returns standard `{"success": false}` and error status code on error

#### PATCH /exercisese/<exercise_id>
Updates an existing exercise
Same json data required as POST /exercises route
Same json return on successful update as the POST /exercise route
Returns standard `{"success": false}` and error status code on error
(returns 404 if exercise_id not found)

#### DELETE /exercises/<exercise_id>
Deletes an existing exercise
No json data needs to be passed in
Returns json and status code (200/404):
```json
{
  "success": true/false,
  "exercise_id": int, id of exercise deleted
}
```

## Future plans
#### Minimum Viable Product
1. Create a separate front-end
2. Create a way to log actual workouts (vs planned workouts)
3. Integrate into front-end
4. Start testing out the app
#### Additional development
1. Create separate table for tracking cardio and skill-based workouts (particularly grappling/striking)
2. Determine how to integrate those tables
3. Integrate this into the UI as well
