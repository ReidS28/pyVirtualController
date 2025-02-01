import { Dpad } from "./dpad.js";
import { Joystick } from "./joystick.js";

export class Controller {
	constructor(containerId, svgPath) {
		const container = document.getElementById(containerId);

		if (!container) {
			throw new Error(`Container with ID "${containerId}" not found.`);
		}

		this.container = container;
		this.togglingEnabled = false;
		this.svgPath = svgPath;
		this.buttons = NaN;
		this.leftJoystick = NaN;
		this.rightJoystick = NaN;
		this.dpad = NaN;

		this.initializeController();
	}

	async initializeController() {
		try {
			const toggleButton = document.createElement("div");
			toggleButton.id = "toggle-button";
			toggleButton.style.top = "calc(1.5% * (1 / 0.7))";
			toggleButton.style.left = "1.5%";
			toggleButton.textContent = "Toggle";
			this.container.appendChild(toggleButton);
			document.getElementById("toggle-button").addEventListener(
				"click",
				function () {
					toggleButton.classList.toggle("active");
					this.togglingEnabled = toggleButton.classList.contains("active");
					this.dpad.updateTogglingEnabled(this.togglingEnabled);
					if (!this.togglingEnabled) {
						this.clearAllButtons();
						this.dpad.clearAllButtons();
					}
				}.bind(this)
			);

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
				"left-joystick-container"
			);
			this.createDivForGroup(
				"right-joystick-container-svg",
				"right-joystick-container"
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

			this.dpad = new Dpad(this.togglingEnabled);
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
		const togglingEnabled = () => this.togglingEnabled;
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

	createDivForGroup(groupId, divId) {
		const group = document.getElementById(groupId);
		if (!group) {
			console.error(`Error: Group with ID '${groupId}' not found.`);
			return;
		}

		const bbox = group.getBoundingClientRect();

		// Create a <div>
		const div = document.createElement("div");
		div.id = divId;
		div.style.position = "absolute";
		div.style.left = `${bbox.left}px`;
		div.style.top = `${bbox.top}px`;
		div.style.width = `${bbox.width}px`;
		div.style.height = `${bbox.height}px`;

		document.body.appendChild(div);
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
