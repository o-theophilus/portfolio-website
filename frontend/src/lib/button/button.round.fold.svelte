<script>
	import { RoundButton } from '.';
	let { open, ...props } = $props();
</script>

<div class="fold" class:open>
	<RoundButton icon="chevron-up" {...props}></RoundButton>
</div>

<style>
	.fold {
		transition: transform 0.2s ease-in-out;
		transform: rotate(180deg);
	}
	.open {
		transform: rotate(0deg);
	}
</style>
