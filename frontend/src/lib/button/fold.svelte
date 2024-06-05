<script>
	import BRound from '$lib/button/round.svelte';
	import Icon from '$lib/icon.svelte';

	export let open;
</script>

<BRound on:click>
	<div class="fold" class:open>
		<Icon icon="chevron_right" />
	</div>
</BRound>

<style>
	.fold {
		transform: rotate(180deg);
		transition: transform var(--trans);
	}
	.open {
		transform: rotate(270deg);
	}
</style>
