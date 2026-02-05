export class Dpad {
    constructor(containerId) {    
        this.addClassToSVGElements(document.getElementById(containerId), "dpad-button");
        
        this.svgButtons = document.querySelectorAll(".dpad-button");
        this.POV = -1;

        this.addButtonListenersToSVGButtons()
    }

    addClassToSVGElements(svgElement, classContent) {
		const svgElements = svgElement.querySelectorAll("*");

		svgElements.forEach((element) => {
			element.classList.add(classContent);
		});
	}

    addButtonListenersToSVGButtons() {
        this.svgButtons.forEach((button) => {
            button.addEventListener("mousedown", () => {
                this.changeButton(true, button);
            });
            button.addEventListener("mouseup", () => {
                this.changeButton(false, button);
            });
        });
    }

    changeButton(mousedown, button = NaN) {
        const buttonValues = {
            "dpad-0-degrees": 0,
            "dpad-45-degrees": 45,
            "dpad-90-degrees": 90,
            "dpad-135-degrees": 135,
            "dpad-180-degrees": 180,
            "dpad-225-degrees": 225,
            "dpad-270-degrees": 270,
            "dpad-315-degrees": 315,
        };
    
        if (mousedown) {
            const buttonValue = buttonValues[button.id];

            if (buttonValue !== this.POV && buttonValue !== undefined) {
                this.clearAllButtons();
                button.classList.add("active");
                this.POV = buttonValue;
            }else if (buttonValue == this.POV && buttonValue !== undefined) {
                this.clearAllButtons();
                button.classList.remove("active");
                this.POV = -1;
            }
        } else {
            if (!window.globalState.buttonTogglingEnabled) {
                this.clearAllButtons();
                this.POV = -1;
            }
        }
    }
    
    clearAllButtons() {
        this.svgButtons.forEach((button) => {
            button.classList.remove("active");
        });
        this.POV = -1;
    }

}
