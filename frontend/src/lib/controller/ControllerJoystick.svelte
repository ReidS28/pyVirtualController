<script lang="ts">
	import type { Snippet } from "svelte";
	import { ControllerConnection } from "./webSocket.svelte";

	interface Props {
		id: number;
		connection: ControllerConnection | null;
		children: Snippet;
	}

	let { children, id, connection }: Props = $props();

	let axes = $state({ x: 0, y: 0 });

	function handleInput(axis: "x" | "y", event: Event) {
		const value = parseFloat((event.target as HTMLInputElement).value);
		axes[axis] = value;

		if (connection) {
			connection.send({
                [`j${id}`]: { 
                    x: axes.x, 
                    y: axes.y 
                }
            });
		}
	}
</script>

<div class="controller-box">
	<div class="content">
		{@render children()}
	</div>

	<hr />

	<div class="controls">
		<div class="slider-group">
			<label for="x-axis-{id}">X: {axes.x.toFixed(2)}</label>
			<input
				type="range"
				id="x-axis-{id}"
				min="-1"
				max="1"
				step="0.01"
				value={axes.x}
				oninput={(e) => handleInput("x", e)}
				class="slider"
			/>
		</div>

		<div class="slider-group">
			<label for="y-axis-{id}">Y: {axes.y.toFixed(2)}</label>
			<input
				type="range"
				id="y-axis-{id}"
				min="-1"
				max="1"
				step="0.01"
				value={axes.y}
				oninput={(e) => handleInput("y", e)}
				class="slider"
			/>
		</div>
	</div>
</div>

<style>
	.controller-box {
		border: 2px solid #444;
		border-radius: 8px;
		padding: 1rem;
		background: #222;
		color: white;
		width: 300px;
		font-family: sans-serif;
	}

	.slider-group {
		display: flex;
		flex-direction: column;
		margin-top: 1rem;
	}

</style>
