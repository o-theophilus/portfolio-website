<script>
	import BRound from '$lib/button/round.svelte';

	let disabled = false;
</script>

<BRound
	icon="angle"
	icon_size="10"
	large
	on:click={() => {
		window.history.back();
		disabled = true;
	}}
	{disabled}
/>
