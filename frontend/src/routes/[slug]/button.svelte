<script>
	import { Button } from '$lib/button';
	import { Icon } from '$lib/macro';

	let { icon = 'edit', onclick, children } = $props();
</script>

<div>
	<Button --button-height="28px" --button-font-size="0.8rem" --button-padding-x="8px" {onclick}>
		<Icon {icon} size="1.4" />
		{@render children()}
	</Button>
</div>
