#!/bin/bash

# 0. Constants
NUM_ROWS=1000
NUM_INSERTS=10
TABLE="users"
NUM_COLS=1

echo "drop table if exists users" | sudo mysql db
INSERT="create table users(id integer auto_increment,"
for i in $(seq 1 $NUM_COLS); do
  INSERT=$INSERT"name$i char(100)"
  if [ $i != $NUM_COLS ];then
    INSERT=$INSERT","
  fi
done
INSERT=$INSERT",primary key(id))"
echo $INSERT | sudo mysql db

START=$(date +%s)
# 1. Delete query
echo "delete from $TABLE" | sudo mysql db

# 2. Build query
for insert in $(seq 1 $NUM_INSERTS); do
  echo -n "insert into $TABLE values "
  for row in $(seq 1 $NUM_ROWS); do 
    let n=($insert-1)*$NUM_ROWS+$row
    echo -n "($n, ";
    for col in $(seq 1 $NUM_COLS); do
      echo -n "'user_"$n"_"$col"'";
      if [ $col != $NUM_COLS ];then
        echo -n ","
      fi
    done
    echo -n ")";
    if [ $row != $NUM_ROWS ];then
      echo -n "," 
    fi
  done
  echo ";"
done > q
# | sudo mysql db
STOP=$(date +%s)
let DIFF=($STOP-$START)
let RECORDS=$NUM_ROWS*$NUM_INSERTS
let SPEED=$RECORDS/$DIFF
echo "Inserted: $RECORDS"
echo "Insert speed: $SPEED rows/s"
