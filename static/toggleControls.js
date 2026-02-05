export class ToggleControls{
    constructor(container, left, top, width, height){

        this.container = container

        this.buttonContainer = NaN
        this.buttonTogglingEnabledButton = NaN;
        this.holdJoysticksButton = NaN;
        this.holdTriggersButton = NaN;

        this.createButtons();

    }

    createButtons(){

        this.buttonContainer = document.createElement("div");
        this.buttonContainer.id = "toggle-buttons-container";

        this.buttonTogglingEnabledButton = document.createElement("div");
        this.buttonTogglingEnabledButton.id = "toggling-enabled-button";
        this.buttonTogglingEnabledButton.classList.add("toggle-control-button")

        this.holdJoysticksButton = document.createElement("div");
        this.holdTriggersButton = document.createElement("div");

        this.container.appendChild(this.buttonContainer);

        this.buttonContainer.appendChild(this.buttonTogglingEnabledButton);

    }

}