# Wordlist-Generator-Python
A Python-Based Code To Generate Wordlist


**CONFIG.JSON**
```
{
  "min_digits": 8,            <-- MIN LENGTH OF PASSWORDS
  "max_digits": 8,            <-- MAX LENGTH OF PASSWORDS
  "delay": 0,                 <-- DELAY IN SECONDS. AS YOUR WISH.
  "cpu_percentage": 100,      <-- CPU PERCENTAGE. Suggested 100
  "num_processes": 1          <-- NUM_PROCESSES. Suggested 1
}
```

**INSTALL MODULES**

Run `pip install -r requirements.txt`



*RUN `main.py` to generate a numeric password wordlist*

Command:`python main.py`


*RUN `chars.py` to generate an alphabetical password wordlist*

Command:`python chars.py`
