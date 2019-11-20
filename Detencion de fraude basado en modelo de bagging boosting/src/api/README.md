# Minimal API template

This script will be used as a starting point for future projects involving Machine Learning Webservices. 


## Dependencies

* Flask
* Flask_restful

## Usage

In a console opened at the project folder type this: 

```bash
python api.py
```

And you should see: 

```bash
 * Serving Flask app "api" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 887-900-667
```

## Running the template

On any brower paste: 
```url
  http://localhost:5000/predictions?feature1=1&feature2=2&feature3=1&feature4=2&feature5=1&feature6=2&feature7=1&feature8=2&feature9=1&feature10=2
```

And as a response, you should see something with this structure: 

```javascript
    {
        "Prediction": 1,
        "Impact": {
            "Feature 10": 0.975,
            "Feature 6": 0.944,
            "Feature 8": 0.92,
            "Feature 1": 0.874,
            "Feature 7": 0.772,
            "Feature 4": 0.772,
            "Feature 2": 0.688,
            "Feature 5": 0.65,
            "Feature 3": 0.591,
            "Feature 9": 0.476
        }
    }
```
