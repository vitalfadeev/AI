function eyeFactory( x, y, w, h, corex, corey, corew, coreh ) {
  var eye = {
    "x": x,
    "y": y,
    "w": w,
    "h": h,
    "corex": corex,
    "corey": corey,
    "corew": corew,
    "coreh": coreh,

    drawEye: function( canvas ) {
      var ctx = canvas.getContext("2d");
      ctx.beginPath();
      ctx.ellipse(this.x, this.y, this.w, this.h, 0, 0, 2 * Math.PI);
      ctx.fillStyle = "white";
      ctx.fill();
      ctx.strokeStyle = "#444";
      ctx.stroke();
    },

    drawEyeCore: function( canvas ) {
      var ctx = canvas.getContext("2d");
      ctx.beginPath();
      ctx.ellipse(this.corex, this.corey, this.corew, this.coreh, 0, 0, 2 * Math.PI);
      ctx.fillStyle = "#333";
      ctx.fill();
      ctx.strokeStyle = "#444";
      ctx.stroke();
    },

    draw: function( canvas ) {
        this.drawEye( canvas );
        this.drawEyeCore( canvas );
    }
  };

  return eye;
};


function layerFactory( x, y, distanceY, w, amount ) {
  var layer = {
    neurons: [],

    draw: function( canvas ) {
        for ( var i=0; i < this.neurons.length; i++ ) {
            var neuron = this.neurons[i];
            neuron.draw( canvas );
        }
    }
  };

  var core_size = w / 3;
  var y = y;

  for ( var i=0; i < amount; i++, y+=distanceY ) {
    layer.neurons.push(
      eyeFactory(
        x, y, w, w,
        x, y, core_size, core_size
      )
    );
  }

  return layer;
}


function brainFactory( canvas_wrapper_id, distanceX, distanceY, neuronW, neuronsAmount ) {
    var maxAmount = Math.max(...neuronsAmount);

    var w = (neuronsAmount.length - 1) * distanceX + neuronW + neuronW;
    var h = (maxAmount - 1) * distanceY + neuronW + neuronW;

    var wrapper = document.getElementById( canvas_wrapper_id );
    var canvas = document.createElement("canvas", { "width":w, "height":h });

    canvas.width = w;
    canvas.height = h;

    wrapper.style.width = w+"px";
    wrapper.style.height = h+"px";

    wrapper.appendChild( canvas );

    //
    var brain = {
        "layers": [],

        draw_link: function( canvas, neuron1, neuron2 ) {
            var ctx = canvas.getContext("2d");
            ctx.beginPath();
            ctx.moveTo(neuron1.x, neuron1.y);
            ctx.lineTo(neuron2.x, neuron2.y);
            ctx.strokeStyle = "#DDD";
            ctx.stroke();
        },

        draw_links: function( canvas, layer1, layer2 ) {
            for ( var i=0, l=layer1.neurons.length; i < l; i++ ) {
                var neuron1 = layer1.neurons[i];

                for ( var i2=0, l2=layer2.neurons.length; i2 < l2; i2++ ) {
                    var neuron2 = layer2.neurons[i2];
                    this.draw_link( canvas, neuron1, neuron2 );
                }
            }
        },

        blink: function( canvas ) {
            var stop = false;

            this.layers.forEach(layer => {
                layer.neurons.forEach(neuron => {
                    if (!neuron.direction)
                        neuron.direction = -1

                    if (!neuron.initial_h)
                        neuron.initial_h = neuron.h;

                    neuron.h += neuron.direction;
                    neuron.coreh += neuron.direction;
                    if (neuron.h <= 0)
                        neuron.coreh = 0;
                    if (neuron.h > 5)
                        neuron.coreh = 5;

                    if (neuron.h <= 0)
                        neuron.direction = 1;

                    if (neuron.h >= neuron.initial_h) {
                        stop = true;
                        delete neuron.initial_h;
                        delete neuron.direction;
                    }
                })
            });

            this.redraw( canvas );
            if (!stop) {
                window.requestAnimationFrame( this.blink.bind( this, canvas ) );
            } else {
                var intervalID = window.setTimeout( () => { window.requestAnimationFrame( this.blink.bind( this, canvas ) ) }, 5000 + Math.floor(Math.random() * Math.floor(10))*1000 );
            }
        },

        draw: function( canvas ) {
            for ( var i=0, l=this.layers.length; i < l; i++ ) {
                var layer = this.layers[i];

                // links
                if (i < l-1) {
                    var layer2 = this.layers[i+1];
                    this.draw_links( canvas, layer, layer2 );
                }

                // neurons
                layer.draw( canvas );
            }
        },

        redraw: function( canvas ) {
            const context = canvas.getContext( '2d');
            context.clearRect(0, 0, canvas.width, canvas.height);
            this.draw( canvas );
        }
    };

    //
    var x = neuronW;

    for (var i=0, l=neuronsAmount.length; i < l; i++, x += distanceX) {
        var amount = neuronsAmount[i];
        var y = neuronW + distanceY * (maxAmount - amount) / 2;
        brain.layers.push( layerFactory( x, y, distanceY, neuronW, amount ) );
    }

    return brain;
}

function update_position( mx, my ) {
    var canvas = document.getElementById( "canvas" ).querySelector('canvas');

    var rect = canvas.getBoundingClientRect();
    var px = rect.left;
    var py = rect.top;

    var w = window.innerWidth
    || document.documentElement.clientWidth
    || document.body.clientWidth;

    var h = window.innerHeight
    || document.documentElement.clientHeight
    || document.body.clientHeight;

    var gravity = 0.8;

    //
    brain.layers.forEach(layer => {
        layer.neurons.forEach(neuron => {
            var cx = px + neuron.x;
            var cy = py + neuron.y;

            // afstand van middenpunt oog tot cursor
            dx = mx - cx;
            dy = my - cy;
            // stelling van pythagoras
            c = Math.sqrt((dx*dx) + (dy*dy));

            // afstand middelpunt tot pupil
            r = neuron.w * gravity;

            // cursor op oog
            if (Math.abs(dx) < r && Math.abs(dy) < r && c < r) {
                r = c;
            }

            // hoek bepalen
            alfa = Math.asin(dy / c);

            // coordinaten op rand cirkel bepalen
            neuron.corex = Math.cos(alfa) * r;

            // 180 graden fout herstellen
            neuron.corex = neuron.x + (dx < 0 ? neuron.corex * -1 : neuron.corex);
            neuron.corey = neuron.y + Math.sin(alfa) * r;
        })
    });

    brain.redraw( canvas );
}


function textWidth( input ) {
    var css = function( element, property ) {
        return window.getComputedStyle( element, null ).getPropertyValue( property );
    }

    var tag = document.createElement("div");
    tag.style.position = "absolute";
    tag.style.left = "-999em";
    tag.style.whiteSpace = "nowrap";
    tag.style.font = css( input, "font" );
    tag.style.padding = input.style.padding;
    tag.style.border = input.style.border;
    tag.innerHTML = input.value;

    document.body.appendChild(tag);

    var result = tag.clientWidth;

    document.body.removeChild(tag);

    return result;
}

function mouse_position( e ) {
    var mx = e.clientX;
    var my = e.clientY;

    update_position( mx, my );
}


function text_position( e ) {
    var input = e.target;

    var rect = input.getBoundingClientRect();

    var mx = rect.left;
    var my = rect.top;

    mx = mx + textWidth( input );

    update_position( mx, my );
}


//
var brain = brainFactory( "canvas", 150, 50, 15, [3, 5, 5, 5, 5, 1]);
var canvas = document.getElementById( "canvas" ).querySelector('canvas');
brain.redraw( canvas );

document.addEventListener('mousemove', mouse_position);

document.getElementById( "id_username" ).addEventListener('keyup', text_position);
document.getElementById( "id_password" ).addEventListener('keyup', text_position);

text_position( {"target": document.getElementById( "id_username" )} );

var intervalID = window.setTimeout( () => { window.requestAnimationFrame( brain.blink.bind( brain, canvas ) ) }, 5000 + Math.floor(Math.random() * Math.floor(10))*1000 );

