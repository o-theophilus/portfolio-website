<script>
	import BRound from '$lib/button/round.svelte';

	let disabled = false;
</script>

<BRound
	icon="arrow_back"
	large
	on:click={() => {
		window.history.back();
		disabled = true;
	}}
	{disabled}
/>
