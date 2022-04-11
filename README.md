# SLAM with Event Camera
![overviewed image](images/overview.png)
This is my YEAR FOUR graduation project about SLAM with event camera.
I implement an event-based particle filtering algorithm to solve the
localization in planar motion problem

*Contributor:* Enming ZHANG

## requirement
- numpy
- bisect
- scipy
- tqdm
- matplotlib
- seaborn

you also can run command
```python
pip install -r requirement.txt
```
## started

clone the repo by
```python
git clone https://github.com/zamling/DB.git
```

## run custom data
prepare the recorded data. I have given the codes about dealing with data in 
ATIS format, you can run `demo_open_data.m`

If you want to get the particles map, you can run
```
python main.py
# optional modes
python main.py --expand --only_pos
```
If you want to get the weight map, you can run
```
python weight.py
# optional modes
python weight.py --expand --only_pos
```
If you want to check some key intermediate values, you can run
```
python debug.py
# optional modes
python weight.py --expand --only_pos --debug_type "cost"/"transform"
```
Note: you need to set your own path in codes

## acknowledgement
Thanks are due to my supervisor, Altmann, Yoann and my teaching assistants 
Hamilton, Craig and Abdulaziz, Abdullah



