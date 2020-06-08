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
Returns standard `{"success": False}` and error status code on error

#### GET /workouts/<workout_id>
Returns a particular workout
No data needs to be passed in (aside from exercise_id in url)
Returns json:
```json
{
  "workout": workout object formatted in json (including exercise list),
  "success": true
}
```
Returns standard `{"success": False}` and error status code on error
(returns 404 if that exercise_id does not exist)

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
Returns standard `{"success": False}` and error status code on error

#### PATCH /workouts/<workout_id>
