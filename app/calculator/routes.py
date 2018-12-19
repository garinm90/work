from math import ceil
from flask import flash, redirect, url_for, render_template, request
from app.calculator.forms import PowerCalculatorForm
from app.calculator import bp


@bp.route('/power_calculator', methods=['GET', 'POST'])
def power_calculator():
    form = PowerCalculatorForm()
    if form.validate_on_submit():
        power = form.nine_led_puck.data * .11 + form.six_led_puck.data * .09
        if power > 0:
            total_two_forty = ceil(power / 10)
        else:
            total_two_forty = None
            power = None
        
        return redirect(url_for('calculator.power_calculator', total_two_forty=total_two_forty))
    total_two_forty = request.args.get('total_two_forty', None)
    return render_template('calculator/calculator.html', form=form, total_two_forty=total_two_forty)