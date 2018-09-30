def get_script(**kwargs):
    return """
    const delay = {delay};
    const variation = {variation};
    const errors = {errors};
""".format(**kwargs) + """
    const total = 20;
    var count = 0;
    var err_count = 0;
    var corr_count = 0;

    const press_space = del => {
        var press_down = new KeyboardEvent('keydown',{'keyCode':32,'which':32});
        setTimeout(
            () => document.dispatchEvent(press_down),
            del,
        );
    };

    const callback = event => {
        console.log(event);

        const is_green = count % 2 == 1;

        var del;
        if (err_count < errors) { //  && corr_count == total - errors // add that to make errors in the end..
            // TODO assert !is_green?
            del = 5;
            count += 2; // mmm...
            err_count += 1;
            console.log("pressing error!")
        } else {
            count += 1;
            if (is_green) {
                del = delay + (Math.random() * variation - variation / 2);
                corr_count += 1;
                console.log("pressing green!");
            } else {
                return;
            }
        }
        press_space(del);
    };

    const e = document.getElementById('simple_reaction_time_stimulus');
    const observer = new MutationObserver(callback);
    // TODO ok I need odd ones
    observer.observe(e, {
        attributes: true,
        attributeFilter: ['class'],
        childList: false,
        characterData: false
    });
    """
