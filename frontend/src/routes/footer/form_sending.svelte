<script>
	import { createEventDispatcher } from 'svelte';
	const dispatch = createEventDispatcher();

	import Button from '$lib/comp/button.svelte';
	export let state = 0;
</script>

<section>
	<div class="blocker">
		{#if state == 1}
			<strong class="big">Sending...</strong>
		{:else}
			<strong class="big">Message Sent</strong>
			<br /><br />
			Thank You
			<br /><br />
			<Button
				class="wide"
				on:click={() => {
					dispatch('closed');
				}}>Close</Button
			>
		{/if}
	</div>
</section>

<style>
	section,
	.blocker {
		display: flex;
		justify-content: center;
		align-items: center;
	}
	section {
		position: absolute;
		inset: -10px;
		z-index: 1;

		backdrop-filter: blur(3px);
	}

	.blocker {
		background-color: var(--accent4);
		gap: var(--gap3);
		flex-direction: column;

		padding: var(--gap4);
		border-radius: var(--gap1);
	}
</style>
