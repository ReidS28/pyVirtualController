<script lang="ts">
	import { onMount } from "svelte";
	import { ControllerConnection } from "./webSocket.svelte";

	interface Props {
		id: string;
		center_x: number;
		center_y: number;
		radius: number;
		connection: ControllerConnection | null;
	}

	let { id, center_x, center_y, radius, connection }: Props = $props();

	let axes = $state({ x: 0, y: 0 });
	let dragging = $state(false);

	onMount(() => {
		const interval = setInterval(() => {
			connection?.send({
				[id]: { x: axes.x, y: axes.y },
			});
		}, 100);

		return () => clearInterval(interval);
	});

	function startDrag(e: PointerEvent) {
		dragging = true;
		(e.currentTarget as HTMLElement).setPointerCapture(e.pointerId);
		handleMove(e);
	}

	function handleMove(e: PointerEvent) {
		if (!dragging && e.type !== "pointerdown") return;

		const rect = (e.currentTarget as HTMLElement).getBoundingClientRect();
		const centerX = rect.left + rect.width / 2;
		const centerY = rect.top + rect.height / 2;

		const dx = e.clientX - centerX;
		const dy = e.clientY - centerY;

		const distance = Math.sqrt(dx * dx + dy * dy);
		const clampedDir = distance > radius ? radius / distance : 1;

		axes.x = (dx * clampedDir) / radius;
		axes.y = -(dy * clampedDir) / radius;

		connection?.send({
			[id]: { x: axes.x, y: axes.y },
		});
	}

	function stopDrag() {
		dragging = false;
		axes = { x: 0, y: 0 };
		connection?.send({ [`j${id}`]: { x: 0, y: 0 } });
	}
</script>

<div
	class="joystick-area"
	role="slider"
	aria-valuemin="-1"
	aria-valuemax="1"
	tabindex="0"
	style="
        left: {center_x}px; 
        top: {center_y}px; 
        width: {radius * 2}px; 
        height: {radius * 2}px;
    "
	onpointerdown={startDrag}
	onpointermove={handleMove}
	onpointerup={stopDrag}
	onpointerleave={stopDrag}
>
	<div
		class="knob"
		style="
            transform: translate(
                calc(-50% + {axes.x * radius}px), 
                calc(-50% + {-axes.y * radius}px)
            );
        "
	></div>
</div>

<style>
	.joystick-area {
		position: absolute;
		background: rgba(255, 255, 255, 0.1);
		border-radius: 50%;
		touch-action: none;
		user-select: none;
		transform: translate(-50%, -50%);
	}

	.knob {
		position: absolute;
		left: 50%;
		top: 50%;
		width: 80%;
		height: 80%;
		background: rgb(32, 89, 136);
		border-radius: 50%;
		pointer-events: none;
		transition: transform 0.05s linear;
	}
</style>
