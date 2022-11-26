#!/bin/sh

echo "STARTING JSON SEQUENCE..."
for i in `seq 0 1 150`
do  
    python scripts/fingerlink.py -t 'JSON' -m $i -d 'time' &&
    python scripts/fingerlink.py -t 'JSON' -m $i -d 'ram' || break
done 

mv ram_usage_data.txt results/json_ram_usage_data.txt
mv elapsed_time_data.txt results/json_elapsed_time_data.txt

echo "STARTING ISO SEQUENCE..."
for i in `seq 0 1 150`
do
    python scripts/fingerlink.py -t 'ISO' -m $i -d 'time' &&
    python scripts/fingerlink.py -t 'ISO' -m $i -d 'ram' || break
done

mv ram_usage_data.txt results/iso_ram_usage_data.txt
mv elapsed_time_data.txt results/iso_elapsed_time_data.txt

echo "STARTING XYT SEQUENCE..."
for i in `seq 0 1 150`
do
    python scripts/fingerlink.py -t 'XYT' -m $i -d 'time' &&
    python scripts/fingerlink.py -t 'XYT' -m $i -d 'ram' || break
done

mv ram_usage_data.txt results/xyt_ram_usage_data.txt
mv elapsed_time_data.txt results/xyt_elapsed_time_data.txt

echo "STARTING PROTOCOL BUFFER SEQUENCE..."
for i in `seq 0 1 150`
do
    python scripts/fingerlink.py -t 'PB' -m $i -d 'time' &&
    python scripts/fingerlink.py -t 'PB' -m $i -d 'ram' || break
done

mv ram_usage_data.txt results/pb_ram_usage_data.txt
mv elapsed_time_data.txt results/pb_elapsed_time_data.txt