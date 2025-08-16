<script>
	import { goto } from '$app/navigation';
	import { RoundButton } from '.';

	let { href = '' } = $props();
	let disabled = $state(false);
</script>

<RoundButton
	icon="arrow-left"
	onclick={() => {
		if (href) {
			goto(href);
		} else {
			window.history.back();
			disabled = true;
		}
	}}
	{disabled}
></RoundButton>
