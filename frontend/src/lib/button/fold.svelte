<script>
	import BRound from '$lib/button/round.svelte';
	import SVG from '$lib/svg.svelte';

	export let open;
</script>

<BRound on:click>
	<div class="fold" class:open>
		<SVG icon="angle" size="8" />
	</div>
</BRound>

<style>
	.fold {
		transition: var(--trans1);
		transform: rotate(180deg);
	}
	.open {
		transform: rotate(270deg);
	}
</style>
