<script>
	import { Button } from '$lib/button';

	let { icon = 'edit', onclick, children } = $props();
</script>

<div>
	<Button
		icon="square-pen"
		--button-height="28px"
		--button-font-size="0.8rem"
		--button-padding-x="8px"
		{onclick}
	>
		{@render children()}
	</Button>
</div>
