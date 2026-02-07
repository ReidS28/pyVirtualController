<script lang="ts">
	import type { Snippet } from "svelte";
	import { ControllerConnection } from "./webSocket.svelte";

	interface Props {
		id: number;
		connection: ControllerConnection | null;
		children: Snippet;
	}

	let { children, id, connection }: Props = $props();

function sendState(isPressed: boolean) {
    if (connection) {
        connection.send({ 
            [`b${id}`]: { pressed: isPressed } 
        });
    }
}
</script>

<button
	onmousedown={() => sendState(true)}
	onmouseup={() => sendState(false)}
>
	{@render children()}
</button>
