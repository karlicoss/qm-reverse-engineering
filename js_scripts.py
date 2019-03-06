SIMPLE_REACTION_SCRIPT = """
    const delay = {delay};
    const variation = {variation};
    const errors = {errors};
""" + """
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
    """.replace('{', '{{').replace('}', '}}')

VISUAL_MATCHING_SCRIPT = """
    const delay = {delay};
    const variation = {variation};
    const errors = {errors};
""" + """

    function matches() {
    var tl = document.getElementById('stimulus_left' ).firstChild.firstChild.firstChild;
    var tr = document.getElementById('stimulus_right').firstChild.firstChild.firstChild;
    for (var i = 0; i < 8; i++) {
        for (var j = 0; j < 8; j++) {
            var cl = tl.children[i].children[j].className;
            var cr = tr.children[i].children[j].className;
            if (cl != cr) {
                return false;
            }
        }
    }
    return true;
    }

    document.getElementById('all_statistics').prepend(document.createTextNode(`simulating ${delay} ms reaction, ${errors} errors`));


    const e = document.getElementById('stimulus_left' );

    var count = 0;
    var err_count = 0;
    var observer = new MutationObserver(function (event) {
        console.log(count);
       if (count % 2 == 0) {
           setTimeout( function () {
                var key = (matches() ^ (errors > err_count)) ? 39 : 37;
                err_count += 1;

                var ee = new KeyboardEvent('keydown',{'keyCode':key,'which':key});
                document.dispatchEvent(ee);
        }, delay + (Math.random() * variation - variation / 2));
       }
       count += 1;
    });

    observer.observe(e, {
      childList: true,
    });
    """.replace('{', '{{').replace('}', '}}')
