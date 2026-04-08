#!/bin/bash

SOURCE_LIST="12 Week Development Plan"

/usr/bin/osascript <<EOF
tell application "Reminders"

    set sourceList to list "$SOURCE_LIST"

    -- Get today's date (Friday)
    set todayDate to current date

    -- Calculate Monday of this week
    set w to weekday of todayDate
    if w is Monday then
        set daysSinceMonday to 0
    else if w is Tuesday then
        set daysSinceMonday to 1
    else if w is Wednesday then
        set daysSinceMonday to 2
    else if w is Thursday then
        set daysSinceMonday to 3
    else if w is Friday then
        set daysSinceMonday to 4
    else if w is Saturday then
        set daysSinceMonday to 5
    else
        set daysSinceMonday to 6
    end if

    set thisMonday to todayDate - (daysSinceMonday * days)
    set time of thisMonday to 0

    -- End of Friday (midnight Saturday)
    set endOfFriday to todayDate + (1 * days)
    set time of endOfFriday to 0

    -- Mark this week's reminders as completed
    set weekReminders to reminders of sourceList whose completed is false and due date ≥ thisMonday and due date < endOfFriday
    repeat with r in weekReminders
        set completed of r to true
    end repeat

end tell
EOF

echo "This week's development reminders marked as completed."
