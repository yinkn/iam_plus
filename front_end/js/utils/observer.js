import Rx from 'rx';
import DOM from 'rx-dom';

var observe = {
    
    start() {
        Rx.Observable.of(1,2,3);
    },
    listen(element, eventName) {
        return new Observable(observer => {
            // Create an event handler which sends data to the sink
            let handler = event => observer.next(event);
    
            // Attach the event handler
            element.addEventListener(eventName, handler, true);
    
            // Return a cleanup function which will cancel the event stream
            return () => {
                // Detach the event handler from the element
                element.removeEventListener(eventName, handler, true);
            };
        });
    },
    commandKeys(element) {
        let keyCommands = { "38": "up", "40": "down" };
    
        return listen(element, "keydown")
            .filter(event => event.keyCode in keyCommands)
            .map(event => keyCommands[event.keyCode])
    },
    onChange() {},
    interval(element) {
        const keyUpStream = Rx.DOM.keyup(element);
        const keyDownStream = Rx.DOM.keydown(element);
        const keyStrokeStream = Rx.Observable.merge(keyDownStream, keyUpStream);
        const keysPressed = {};
        const keysPressedRecords =  [];

        keyStrokeStream.subscribe(event => {
            const key = event.code;
            if (event.type == 'keyup' && keysPressed.hasOwnProperty(key)) {
                const newRecord = {key, keyCode: event.keyCode};
                newRecord.end = Date.now();
                newRecord.start = keysPressed[key];
                newRecord.duration =  newRecord.end - newRecord.start;

                console.info(newRecord);
                keysPressedRecords.push(newRecord);

                delete keysPressed[key];
            } else if (event.type == 'keydown') {
                if (!keysPressed.hasOwnProperty(key)) {
                    keysPressed[key] = Date.now();
                }
            }
        });

        return keysPressedRecords;
    }
  }
  
  module.exports = observe;
