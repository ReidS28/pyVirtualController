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
                target.classList.add("pressed");
                target.setPointerCapture(event.pointerId);
            } else {
                target.classList.remove("pressed");
                target.releasePointerCapture(event.pointerId);
            }

            if (connection) {
                connection.send({
					[key]: { 
						pressed: isPressed 
					}
				});
            }
        }else{
			console.log(key)
		}
    }
</script>

<div 
    class="controller-wrapper"
    onpointerdown={(e) => handleAction(e, true)}
    onpointerup={(e) => handleAction(e, false)}
    onpointerleave={(e) => handleAction(e, false)} 
>
    {@html ds4SVG}
</div>

<style>
    .controller-wrapper {
        width: 100%;
        max-width: 600px;
        margin: auto;
        touch-action: none;
        user-select: none;
    }

    :global(.controller-wrapper svg) {
        width: 100%;
        height: auto;
    }

    :global(.controller-wrapper [data-key^="b"]) {
        cursor: pointer;
        transition: fill 0.1s;
    }

    :global(.controller-wrapper .pressed) {
        fill: #ff3e00 !important;
        stroke: white !important;
        stroke-width: 0.5px;
    }
</style>