<script>
	import { goto } from '$app/navigation';
	import { Icon } from '$lib/macro';
	import { RoundButton } from '.';

	let { href = '' } = $props();
	let disabled = $state(false);
</script>

<RoundButton
	onclick={() => {
		if (href) {
			goto(href);
		} else {
			window.history.back();
			disabled = true;
		}
	}}
	{disabled}
>
	<Icon icon="arrow_back"></Icon>
</RoundButton>
