<script>
	import { RoundButton } from '.';
	import { Icon } from '$lib/macro';
	let { open, ...props } = $props();
</script>

<div class="fold" class:open>
	<RoundButton {...props}>
		<Icon icon="keyboard_arrow_up"></Icon>
	</RoundButton>
</div>

<style>
	.fold {
		transition: transform var(--trans);
		transform: rotate(180deg);
	}
	.open {
		transform: rotate(0deg);
	}
</style>
