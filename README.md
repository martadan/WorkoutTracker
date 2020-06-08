# WorkoutTracker


## Overview
<p>There are already loads of fitness apps, but most do not have the flexibility to track different styles of workouts in the same app.
I decided to build one out myself to allow the flexibility I want without all the extra features I don't need</p>

<p>Published live at:<br>
(TODO add url here)</p>


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
