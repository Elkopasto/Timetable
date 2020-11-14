# Timetable
Timetable - a place to manage school schedule.

UI:
 * Main window
 * Teachers windows
 * Grades window

------------------------------------------------------------------------------------------------------------------------

    Teachers window: You can edit list of teachers, and the subjects they teach.
    Grades window: You can manage a list of how many of every subject grade needs per week.
    Main window: You can initiate a schedule calculation, view and drop the schedule for every class and weekday.

------------------------------------------------------------------------------------------------------------------------

Features:
 + Teachers to subjects - many to many relationship
 + Validation exists that total hours per week for each grade doesn't exceed a limit of 30 hours
 + Schedule is created automatically by an algorithm 
 + Unique indexes on schedule table ensure that no class and no teacher has two lessons on same time