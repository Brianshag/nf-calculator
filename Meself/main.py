from flask import Flask
from flask import request
import NFCalculator

app = Flask(__name__)

@app.route("/")
def index():
    nSOff = request.args.get("nSOff", "")
    nSOn = request.args.get("nSOn", "")
    nSOff_DUT = request.args.get("nSOff_DUT", "")
    nSOn_DUT = request.args.get("nSOn_DUT", "")
    enr = request.args.get("enr", "")
    NF = calcNF(nSOff, nSOn, nSOff_DUT, nSOn_DUT, enr)
    return(
        """<form action="" method="get">
                <input type="text" name="nSOff">
                <input type="text" name="nSOn">
                <input type="text" name="nSOff_DUT">
                <input type="text" name="nSOn_DUT">
                <input type="text" name="enr">
                <input type="submit" value="Calculate">
              </form>"""
        + "The Noise Figure is: "
        + NF  # this is the output after the request to get user input value for each prompt is taken
    )
    
def calcNF(nSOff, nSOn, nSOff_DUT, nSOn_DUT, enr):
    try:    # the try and except block is needed because when i first load the page, all the required prompts are empty strings, and you cant convert empty string to int, and the NF script wont execute. So once it loads the page first time, it "tries", and gives "invalid input", and then i can try again on same page
        return str(NFCalculator.NF(float(nSOff), float(nSOn), float(nSOff_DUT), float(nSOn_DUT), float(enr)))
    except ValueError:
        try:
            nSOff_f     = float(nSOff)
            nSOn_f      = float(nSOn)
            nSOff_DUT_f = float(nSOff_DUT)
            nSOn_DUT_f  = float(nSOn_DUT)

            if nSOff_DUT_f < nSOff_f:
                return "Noise Source + DUT in off-state cannot be a higher value than Noise Source only in off-state"
            elif nSOn_DUT_f < nSOn_f:
                return "Noise Source + DUT in on-state cannot be a higher value than Noise Source only in on-state"
            else:
                return "invalid input"
        except ValueError:
            return "invalid input"

        
    #return str(NFCalculator.NF(-92, -87, -103, -92, 15))


# @app.route("/")
# def index():
#     celsius = request.args.get("celsius", "") # fetches user input value. Will return empty string if no input submitted
#     if celsius:
#         fahrenheit = fahrenheit_from(celsius)
#     else:
#         fahrenheit = ""
#     return (
#         """<form action="" method="get">
#                 Celsius temperature: <input type="text" name="celsius">
#                 <input type="submit" value="Convert to Fahrenheit">
#             </form>"""
#         + "Fahrenheit: "
#         + fahrenheit            # returns the user inputted value which goes through if/else
#     )

# def fahrenheit_from(celsius):
#     """Convert Celsius to Fahrenheit degrees."""
#     try:
#         fahrenheit = float(celsius) * 9 / 5 + 32
#         fahrenheit = round(fahrenheit, 3)  # Round to three decimal places
#         return str(fahrenheit)
#     except ValueError:
#         return "invalid input"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)