<script lang="ts">
    import { onMount, onDestroy } from "svelte";
    import { ControllerConnection } from "./webSocket.svelte";
    import ds4SVG from "../../assets/ds4-controller.svg?raw";

    interface Props {
        controllerID: number;
    }

    let { controllerID }: Props = $props();
    let connection: ControllerConnection | null = $state(null);

    onMount(() => {
        connection = new ControllerConnection(controllerID);
    });

    onDestroy(() => {
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
						pressed: isPressed 
					}
				});
            }
        }else if (key && key.startsWith("d")){
			let angle: number = isPressed? +key.replace("d", "0") : -1;
			
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
						angle: angle 
					}
				});
            }
		}
    }
</script>

<div 
    class="controller-wrapper"
    role="application"
    aria-label="Game Controller"
    onpointerdown={(e) => handleAction(e, true)}
    onpointerup={(e) => handleAction(e, false)}
    onpointerleave={(e) => handleAction(e, false)}
>
	Controller {controllerID}
    {@html ds4SVG}
</div>

<style>
    .controller-wrapper {
        width: 100%;
        margin: auto;
        touch-action: none;
        user-select: none;
		background-color: rgba(61, 61, 70, 0.434);
		border-style: solid;
		border-color: #1C1C1C;
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
        transition: fill 0.1s, stroke 0.1s;
    }

    :global(.controller-wrapper .active) {
        fill: #24019631 !important; 
        stroke: #00033E !important;
        stroke-width: 0.5px;
    }
</style>