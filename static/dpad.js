export class Dpad {
    constructor(containerId, svgPath, togglingEnabled = false) {
        const container = document.getElementById(containerId);
        
        if (!container) {
            throw new Error(`Container with ID "${containerId}" not found.`);
        }
        
        this.container = container;
        this.svgPath = svgPath;
        this.togglingEnabled = togglingEnabled;
        this.svgButtons = NaN;
        this.POV = 0;
        
        this.embedSVG();
    }
    
    updateToggling(enabled) {
        this.togglingEnabled = enabled;
    }

    async embedSVG() {
        try {
            const response = await fetch(this.svgPath);
            const svgText = await response.text();

            const parser = new DOMParser();
            const svgDoc = parser.parseFromString(svgText, "image/svg+xml");
            const svgElement = svgDoc.documentElement;

            svgElement.setAttribute("width", "100%");
            svgElement.setAttribute("height", "100%");

            this.container.innerHTML = "";
            this.container.appendChild(svgElement);

            this.addClassToSVGButtons(svgElement);
            this.addButtonListenersToSVGButtons(svgElement);

        } catch (error) {
            console.error("Error loading SVG:", error);
        }
    }

    addClassToSVGButtons(svgElement) {
        const svgButtons = svgElement.querySelectorAll('*');

        svgButtons.forEach((button) => {
            button.classList.add("dpad-button");
        });
    }

    addButtonListenersToSVGButtons(svgElement) {
        this.svgButtons = svgElement.querySelectorAll('*');

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
            }
        } else {
            if (!this.togglingEnabled) {
                this.clearAllButtons();
                this.POV = -1;
            }
        }
    }
    
    

    clearAllButtons() {
        this.svgButtons.forEach((button) => {
            button.classList.remove("active");
        });
        this.POV = 0;
    }

}
