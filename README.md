# Movie Theater Seating Challenge

This assingment implements an algorithm for assigning seats within a movie theater to fulfill reservation requests. The movie theater is assumed to have a 10 row by 20 seat layout. The goal of this is to write a program that maximizes customer satisfaction and customer safety, during COVID-19 times. There must be a buffer of three seets and/or one row between groups.

## Assumptions

There were several assumptions I made for this program.

* I did some research and concluded that the most desirable seats in a movie theater are the middle-back seats, and the middle seats in general. With this in mind, I assigned weights to the movie theater seats where the middle are the best, and the value decrements as you approach the left and right aisles. Extra value for any seat in the back half.

* Also assumed that every seat cost the same amount. 

* To maximize customer satisfaction, I assumed that being seated together and having the best possible seats according to my weightings were the decision making factors for this metric. The preference was to first try and group them together, then maximize the seating value.

* The document said there should be a three seat buffer and/or one row between groups. I interpreted this as groups can be directly seated behind/in front of other groups if they are in a different row, but if they are in the same row they must be three seats apart. If this isn't the case the program can still be easily modified to account for needed precautions.

## Program Description

The core of this program uses a priority queue with a greedy algorithm. Since the reservations are in a queue, they will be given the best possible experience in the order the reservations were recieved. This is why a greedy algorithm is a great use for this application because each customer deserves the best available at the time of their booking. The greedy algorithm simply places them in the best position available. 

### Executing program

* How to run the program
* Step-by-step bullets
```
code blocks for commands
```
