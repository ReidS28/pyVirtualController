import { Dpad } from "./dpad.js";
import { Joystick } from "./joystick.js";
import { ToggleControls } from "./toggleControls.js";

export class Controller {
	constructor(containerId, svgPath) {
		const container = document.getElementById(containerId);

		if (!container) {
			throw new Error(`Container with ID "${containerId}" not found.`);
		}

		this.container = container;
		this.svgPath = svgPath;
		this.buttons = NaN;
		this.leftJoystick = NaN;
		this.rightJoystick = NaN;
		this.dpad = NaN;

		this.initializeController();
	}

	async initializeController() {
		try {
			/*const toggleButton = document.createElement("div");
			toggleButton.id = "toggle-button";
			toggleButton.style.top = "calc(1.5% * (1 / 0.7))";
			toggleButton.style.left = "1.5%";
			toggleButton.textContent = "Toggle";
			this.container.appendChild(toggleButton);
			document.getElementById("toggle-button").addEventListener(
				"click",
				function () {
					toggleButton.classList.toggle("active");
					window.globalState.buttonTogglingEnabled = toggleButton.classList.contains("active");
					if (!window.globalState.buttonTogglingEnabled) {
						this.clearAllButtons();
						this.dpad.clearAllButtons();
					}
				}.bind(this)
			);*/
			const toggleControls = new ToggleControls(this.container, "calc(1.5% * (1 / 0.7))", "1.5", 100, 100);

			const response = await fetch(this.svgPath);
			const svgText = await response.text();

			const parser = new DOMParser();
			const svgDoc = parser.parseFromString(svgText, "image/svg+xml");
			const svgElement = svgDoc.documentElement;

			svgElement.setAttribute("width", "100%");
			svgElement.setAttribute("height", "100%");

			this.container.appendChild(svgElement);

			this.addClassToSVGElements(document.getElementById("buttons"), "button");
			this.buttons = document.querySelectorAll(".button");

			this.addEventListeners(this.buttons);

			this.createDivForGroup(
				"left-joystick-container-svg",
				"left-joystick-container",
				"joystick-container"
			);
			this.createDivForGroup(
				"right-joystick-container-svg",
				"right-joystick-container", 
				"joystick-container"
			);

			this.leftJoystick = new Joystick(
				"left-joystick-container",
				-1.0,
				0.0,
				1.0,
				-1.0,
				0.0,
				1.0
			);
			this.rightJoystick = new Joystick(
				"right-joystick-container",
				-1.0,
				0.0,
				1.0,
				-1.0,
				0.0,
				1.0
			);

			this.dpad = new Dpad("dpad-buttons");
		} catch (error) {
			console.error("Error loading SVG:", error);
		}
	}

	addClassToSVGElements(svgElement, classContent) {
		const svgElements = svgElement.querySelectorAll("*");

		svgElements.forEach((element) => {
			element.classList.add(classContent);
		});
	}

	addEventListeners(elements) {
		const togglingEnabled = () => window.globalState.buttonTogglingEnabled;
		elements.forEach((element) => {
			element.addEventListener("mousedown", function () {
				if (togglingEnabled()) {
					element.classList.toggle("active");
				} else {
					element.classList.add("active");
				}
			});
			element.addEventListener("mouseup", function () {
				if (!togglingEnabled()) {
					element.classList.remove("active");
				}
			});
		});
	}

	clearAllButtons() {
		this.buttons.forEach((button) => {
			button.classList.remove("active");
		});
	}

	createDivForGroup(groupId, divId, className = NaN) {
		const group = document.getElementById(groupId);
		if (!group) {
			console.error(`Error: Group with ID '${groupId}' not found.`);
			return;
		}
	
		const groupBBox = group.getBoundingClientRect();
		const containerBBox = this.container.getBoundingClientRect(); // Get container's absolute position
	
		const div = document.createElement("div");
		div.id = divId;
		if (className !== NaN) div.classList.add(String(className));
	
		div.style.position = "absolute";
		div.style.left = `${groupBBox.left - containerBBox.left}px`;
		div.style.top = `${groupBBox.top - containerBBox.top}px`;
		div.style.width = `${groupBBox.width}px`;
		div.style.height = `${groupBBox.height}px`;
	
		this.container.appendChild(div);
	}
	
	getControllerState() {
		let buttonStates = {};
		if (this.buttons) {
			this.buttons.forEach((button) => {
				buttonStates[button.id] = button.classList.contains("active");
			});
		}

		let controllerStates = {
			// Declare with 'let' or 'const'
			left_x: this.leftJoystick.x,
			left_y: this.leftJoystick.y * -1,
			right_x: this.rightJoystick.x,
			right_y: this.rightJoystick.y * -1,
			buttons: buttonStates,
			dpad: this.dpad.POV,
		};

		return controllerStates;
	}
}
