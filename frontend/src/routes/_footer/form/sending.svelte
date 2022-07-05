<script>
	import { createEventDispatcher } from 'svelte';
	const dispatch = createEventDispatcher();
	export let state = 1;
</script>

<div class="blocker">
	{#if state == 1}
		<h1>Sending...</h1>
	{:else}
		<h1>Message Sent</h1>
		<p>Thank You</p>
			<!-- Feel free to contact me with questions or anything else. I will do my best to respond to your query
                as soon as possible. -->
		<button on:click={() => dispatch('closed')}>Close</button>
	{/if}
</div>

<style>
	.blocker {
		position: absolute;
		inset: -10px;
		z-index: 1;

		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;

		background-color: rgba(56, 56, 56, 0.9);
		backdrop-filter: blur(3px);

		color: var(--color1);
	}
	button {
		--inputHeight: 40px;
		
		width: 100px;
		height: var(--inputHeight);

		padding: 10px;

		border: 2px solid var(--color1);
		border-radius: calc(var(--inputHeight) / 2);

		font-family: var(--font1);
		font-size: 1.2rem;

		color: var(--color1);
		background-color: transparent;

		transition: all var(--animTime1);
		transition-timing-function: ease-in-out;
	}

	button:hover {
		background-color: var(--color3);
		border-color: transparent;
	}
</style>
