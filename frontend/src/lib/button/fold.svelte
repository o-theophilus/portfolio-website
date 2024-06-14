<script>
	import BRound from '$lib/button/round.svelte';
	export let open;
</script>

<div class="fold" class:open>
	<BRound on:click icon="keyboard_arrow_up" />
</div>

<style>
	.fold {
		transition: transform var(--trans);
	}
	.open {
		transform: rotate(180deg);
	}
</style>
