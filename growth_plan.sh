#!/bin/bash

LIST_NAME="12 Week Development Plan"
START_DATE="2026-02-23"

/usr/bin/osascript <<EOF
tell application "Reminders"
    if not (exists list "$LIST_NAME") then
        make new list with properties {name:"$LIST_NAME"}
    end if
end tell
EOF

add_task() {
    TITLE="$1"
    YEAR="$2"
    MONTH="$3"
    DAY="$4"

    /usr/bin/osascript <<EOF
tell application "Reminders"
    tell list "$LIST_NAME"
        set dueDate to current date
        set year of dueDate to $YEAR
        set month of dueDate to $MONTH
        set day of dueDate to $DAY
        set hours of dueDate to 9
        set minutes of dueDate to 0
        set seconds of dueDate to 0
        make new reminder with properties {name:"$TITLE", due date:dueDate}
    end tell
end tell
EOF
}

current_date=$(date -j -f "%Y-%m-%d" "$START_DATE" +"%s")

for week in {1..12}
do
    for day in {0..4}
    do
        task_epoch=$((current_date + day*86400))
        task_year=$(date -r $task_epoch +"%Y")
        task_month=$(date -r $task_epoch +"%-m")
        task_day=$(date -r $task_epoch +"%-d")

        case $week-$day in

        # WEEK 1
        1-0) task="Week 1: Choose and document a key ownership area (Proactivity & Ownership)" ;;
        1-1) task="Week 1: Draft a one-page initiative outline (Proactivity & Ownership)" ;;
        1-2) task="Week 1: Finalize scope with clear milestones (Structured Execution)" ;;
        1-3) task="Week 1: Share initiative scope with the team (Visibility & Leadership Signal)" ;;
        1-4) task="Week 1: Post first weekly async status update (Visibility & Communication)" ;;

        # WEEK 2
        2-0) task="Week 2: Break initiative into actionable work items (Execution Discipline)" ;;
        2-1) task="Week 2: Schedule cross-team alignment session (Collaboration Expansion)" ;;
        2-2) task="Week 2: Surface one key risk early in planning (Early Risk Signaling)" ;;
        2-3) task="Week 2: Identify a quick-win opportunity (Delivery Momentum)" ;;
        2-4) task="Week 2: Deliver a quick-win improvement (Execution & Speed)" ;;

        # WEEK 3
        3-0) task="Week 3: Document and share improvement impact (Visibility & Narrative)" ;;
        3-1) task="Week 3: Time-box one task to avoid over-optimization (Speed Calibration)" ;;
        3-2) task="Week 3: Align speed vs quality approach during planning (Delivery Strategy)" ;;
        3-3) task="Week 3: Schedule monthly product context sync (Product Awareness)" ;;
        3-4) task="Week 3: Post weekly async status update (Consistency & Visibility)" ;;

        # WEEK 4
        4-0) task="Week 4: Prepare a short design walkthrough (Technical Leadership)" ;;
        4-1) task="Week 4: Facilitate initiative discussion session (Influence & Ownership)" ;;
        4-2) task="Week 4: Capture and share decisions (Clarity & Alignment)" ;;
        4-3) task="Week 4: Contribute beyond assigned ticket scope (Collaboration Depth)" ;;
        4-4) task="Week 4: Reflect on speed vs detail trade-offs (Execution Maturity)" ;;

        # WEEK 5
        5-0) task="Week 5: Map system pain points end-to-end (System-Level Thinking)" ;;
        5-1) task="Week 5: Gather team input on recurring breakpoints (Product Context Expansion)" ;;
        5-2) task="Week 5: Propose a small process improvement (Proactive Improvement)" ;;
        5-3) task="Week 5: Implement the process improvement (Execution Ownership)" ;;
        5-4) task="Week 5: Share an improvement summary (Impact Communication)" ;;

        # WEEK 6
        6-0) task="Week 6: Identify an over-engineered task to simplify (Speed Optimization)" ;;
        6-1) task="Week 6: Deliver a simplified iteration (Pragmatic Delivery)" ;;
        6-2) task="Week 6: Raise one improvement idea in retro (Visible Contribution)" ;;
        6-3) task="Week 6: Run progress check-in with stakeholders (Ownership Continuity)" ;;
        6-4) task="Week 6: Document measurable impact (Results Orientation)" ;;

        # WEEK 7
        7-0) task="Week 7: Identify a reliability gap or resilience opportunity (Reliability Leadership)" ;;
        7-1) task="Week 7: Draft a mini reliability proposal (Technical Initiative)" ;;
        7-2) task="Week 7: Present reliability idea informally (Influence & Advocacy)" ;;
        7-3) task="Week 7: Implement a small reliability experiment (Engineering Ownership)" ;;
        7-4) task="Week 7: Share experiment results (Transparency & Visibility)" ;;

        # WEEK 8
        8-0) task="Week 8: Review CI/CD pipeline end-to-end (Operational Depth)" ;;
        8-1) task="Week 8: Identify two operational inefficiencies (Analytical Thinking)" ;;
        8-2) task="Week 8: Share inefficiency findings across teams (Cross-Team Awareness)" ;;
        8-3) task="Week 8: Prototype or fix one inefficiency (Execution Momentum)" ;;
        8-4) task="Week 8: Document CI/CD outcome (Operational Impact Narrative)" ;;

        # WEEK 9
        9-0) task="Week 9: Clarify next-level ownership expectations with leadership (Strategic Alignment)" ;;
        9-1) task="Week 9: Integrate leadership input into execution plan (Growth Mindset)" ;;
        9-2) task="Week 9: Lead a milestone discussion (Visible Leadership)" ;;
        9-3) task="Week 9: Mentor a peer on a technical topic (Leverage & Enablement)" ;;
        9-4) task="Week 9: Publish cumulative impact summary (Impact Narrative)" ;;

        # WEEK 10
        10-0) task="Week 10: Identify the next improvement domain (Forward Ownership)" ;;
        10-1) task="Week 10: Draft a mini proposal (Strategic Thinking)" ;;
        10-2) task="Week 10: Socialize proposal early (Stakeholder Influence)" ;;
        10-3) task="Week 10: Deliver a fast-iteration improvement intentionally (Delivery Calibration)" ;;
        10-4) task="Week 10: Track and record improvement metrics (Results Measurement)" ;;

        # WEEK 11
        11-0) task="Week 11: Document key initiative outcomes clearly (Impact Documentation)" ;;
        11-1) task="Week 11: Quantify stability and speed gains (Business Impact Awareness)" ;;
        11-2) task="Week 11: Share impact summary with stakeholders (Visibility Scaling)" ;;
        11-3) task="Week 11: Collect peer input explicitly (Feedback Integration)" ;;
        11-4) task="Week 11: Reflect on execution maturity progress (Self-Calibration)" ;;

        # WEEK 12
        12-0) task="Week 12: Write full 12-week impact summary (Delivery Review)" ;;
        12-1) task="Week 12: Run structured retrospective with stakeholders (Continuous Improvement)" ;;
        12-2) task="Week 12: Define next-step calibration plan (Strategic Advancement)" ;;
        12-3) task="Week 12: Identify next ownership area (Long-Term Growth)" ;;
        12-4) task="Week 12: Publish final 12-week update (Executive Communication)" ;;

        esac

        add_task "$task" "$task_year" "$task_month" "$task_day"
    done

    current_date=$((current_date + 7*86400))
done

echo "All 60 tagged development tasks created successfully."
