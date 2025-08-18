<script>
	import { RoundButton } from '$lib/button';

	let { show_password: show = $bindable() } = $props();
</script>

<form onsubmit={(e) => e.preventDefault()} >
	<RoundButton
		icon={show ? 'eye' : 'eye-off'}
		extra="hover_red"
		tabindex="-1"
		onclick={() => {
			show = !show;
		}}
	/>
</form>

<style>
	form {
		display: flex;
		align-items: center;

		height: 100%;
	}
</style>
