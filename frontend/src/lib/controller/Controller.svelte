<script lang="ts">
	import { onMount, onDestroy, tick } from "svelte";
	import { ControllerConnection } from "./webSocket.svelte";
	import ds4SVG from "../../assets/ds4-controller.svg?raw";
	import Joystick from "./Joystick.svelte";

	interface Props {
		controllerID: number;
	}

	let { controllerID }: Props = $props();
	let connection: ControllerConnection | null = $state(null);

	type JoystickOverlay = {
		id: string;
		x: number;
		y: number;
		width: number;
		height: number;
	};

	let wrapper: HTMLDivElement;
	let joysticks: JoystickOverlay[] = $state([]);

	function refreshJoystickPositions() {
		const svg = wrapper.querySelector("svg");
		if (!svg || !wrapper) return;

		const containerRect = wrapper.getBoundingClientRect();

		const borderLeft = wrapper.clientLeft;
		const borderTop = wrapper.clientTop;

		const elements =
			svg.querySelectorAll<SVGGraphicsElement>('[data-key^="j"]');

		joysticks = Array.from(elements).map((el) => {
			const rect = el.getBoundingClientRect();

			return {
				id: el.getAttribute("data-key")!,
				// Subtract the border thickness so '0,0' aligns with the inner corner
				x: rect.left - containerRect.left - borderLeft + rect.width / 2,
				y: rect.top - containerRect.top - borderTop + rect.height / 2,
				width: rect.width,
				height: rect.height,
			};
		});
	}

	onMount(() => {
		connection = new ControllerConnection(controllerID);
		refreshJoystickPositions();
		window.addEventListener("resize", refreshJoystickPositions);
	});

	onDestroy(() => {
		window.removeEventListener("resize", refreshJoystickPositions);
		if (connection) connection.close();
	});

	function handleAction(event: PointerEvent, isPressed: boolean) {
		const target = event.target as SVGElement;
		const key = target?.getAttribute("data-key");

		if (key && key.startsWith("b")) {
			event.preventDefault();
			if (isPressed) {
				target.classList.add("active");
				target.setPointerCapture(event.pointerId);
			} else {
				target.classList.remove("active");
				target.releasePointerCapture(event.pointerId);
			}

			if (connection) {
				connection.send({
					[key]: {
						pressed: isPressed,
					},
				});
			}
		} else if (key && key.startsWith("d")) {
			let angle: number = isPressed ? +key.replace("d", "0") : -1;

			if (isPressed) {
				target.classList.add("active");
				target.setPointerCapture(event.pointerId);
			} else {
				target.classList.remove("active");
				target.releasePointerCapture(event.pointerId);
			}

			if (connection) {
				connection.send({
					["dpad"]: {
						angle: angle,
					},
				});
			}
		} else {
			console.log(key);
		}
	}
</script>

<div
	bind:this={wrapper}
	class="controller-wrapper"
	role="application"
	aria-label="Game Controller"
	onpointerdown={(e) => handleAction(e, true)}
	onpointerup={(e) => handleAction(e, false)}
	onpointerleave={(e) => handleAction(e, false)}
>
	{@html ds4SVG}

	{#each joysticks as j}
		<Joystick
			id={j.id}
			center_x={j.x}
			center_y={j.y}
			radius={Math.min(j.width, j.height) / 2}
			{connection}
		/>
	{/each}
</div>

<style>
	.controller-wrapper {
		position: relative;
		width: 100%;
		margin: auto;
		touch-action: none;
		user-select: none;
		background-color: rgba(61, 61, 70, 0.434);
		border-style: solid;
		border-color: #1c1c1c;
		border-width: 0.4vw;
		border-radius: 5vw;
	}

	:global(.controller-wrapper svg) {
		width: 100%;
		height: auto;
	}

	:global(.controller-wrapper [data-key]) {
		fill: transparent;
		pointer-events: all;
		cursor: pointer;
		transition:
			fill 0.1s,
			stroke 0.1s;
	}

	:global(.controller-wrapper .active) {
		fill: #24019631 !important;
		stroke: #00033e !important;
		stroke-width: 0.5px;
	}

	.controller-wrapper {
		position: relative;
	}
</style>
