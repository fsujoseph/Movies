# Movie Theater Seating Challenge

This assingment implements an algorithm for assigning seats within a movie theater to fulfill reservation requests. The movie theater is assumed to have a 10 row by 20 seat layout. The goal of this is to write a program that maximizes customer satisfaction and customer safety, during COVID-19 times. There must be a buffer of three seets and/or one row between groups.

## Assumptions

There were several assumptions I made for this program.

* I did some research and concluded that the most desirable seats in a movie theater are the middle-back seats, and the middle seats in general. With this in mind, I assigned weights to the movie theater seats where the middle are the best, and the value decrements as you approach the left and right aisles. Extra value for any seat in the back half.

* Also assumed that every seat cost the same amount. 

* To maximize customer satisfaction, I assumed that being seated together and having the best possible seats according to my weightings were the decision making factors for this metric. The preference was to first try and group them together, then maximize the seating value.

* The document said there should be a three seat buffer and/or one row between groups. I interpreted this as groups can be directly seated behind/in front of other groups if they are in a different row, but if they are in the same row they must be three seats apart. If this isn't the case the program can still be easily modified to account for needed precautions.

## Program Description

To start off, an input file is loaded in with a reservation ID and the number of seats requested, as a dictionary (hash map). The input file is called 'reservations.txt'.

A 2-D matrix is initialized at the start of the program which represents the movie theater layout. The seat value weights are assigned at this stage as well. Modularity was kept in mind as any size movie theater can be used and still have a functioning program.

The core logic of this program uses a priority queue with a greedy algorithm. Since the reservations are in a queue, they will be given the best possible experience in the order the reservations were recieved. This is why a greedy algorithm is a great use for this application because each customer deserves the best available at the time of their booking. The greedy algorithm simply places them in the best position available.

If there isn't a slot available for the entire group to fit, the algorithm will attempt to remove a member and try again so that as much of the group will be placed together as possible. The process will be repeated until the entire reservation has a seat, even if they all have individual seats.

Finally, the reservation ID and corresponding seat assignments are stored in a dictionary and exported to a file called 'assignments.txt' to represent seating assignments.

### Executing program

* How to run the program
* Step-by-step bullets
```
code blocks for commands
```
