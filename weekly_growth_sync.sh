#!/bin/bash

SOURCE_LIST="12 Week Development Plan"

/usr/bin/osascript <<EOF
tell application "Reminders"

    set sourceList to list "$SOURCE_LIST"

    -- Get today's date
    set todayDate to current date

    -- Calculate next Monday
    set w to weekday of todayDate
    if w is Sunday then
        set daysUntilMonday to 1
    else if w is Monday then
        set daysUntilMonday to 7
    else if w is Tuesday then
        set daysUntilMonday to 6
    else if w is Wednesday then
        set daysUntilMonday to 5
    else if w is Thursday then
        set daysUntilMonday to 4
    else if w is Friday then
        set daysUntilMonday to 3
    else
        set daysUntilMonday to 2
    end if

    set nextMonday to todayDate + (daysUntilMonday * days)
    set time of nextMonday to 0

    set dayNames to {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday"}

    repeat with i from 1 to 5

        set targetDate to nextMonday + ((i - 1) * days)
        set nextDate to targetDate + (1 * days)
        set dayName to item i of dayNames

        -- Create weekday list if it doesn't exist
        if not (exists list dayName) then
            make new list with properties {name:dayName}
        end if

        set targetList to list dayName

        -- Fetch reminders due on that specific date
        set dayReminders to reminders of sourceList whose due date ≥ targetDate and due date < nextDate

        repeat with r in dayReminders
            set reminderName to name of r

            -- Avoid duplicates
            set existing to reminders of targetList whose name is reminderName
            if (count of existing) is 0 then
                make new reminder at targetList with properties {name:reminderName}
            end if
        end repeat

    end repeat

end tell
EOF

echo "Weekly development tasks synced successfully."
