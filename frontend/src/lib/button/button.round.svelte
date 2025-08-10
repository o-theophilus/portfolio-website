<script>
	import { Button } from '.';
	import { Icon2 } from '$lib/macro';

	let { icon, ...props } = $props();
</script>

<Button
	{...props}
	--button-padding-x="0"
	--button-width="32px"
	--button-height="32px"
	--button-border-radius="50%"
	--button-color="var(--ft1)"
	--button-background-color="var(--bg2)"
>
	<Icon2 {icon}></Icon2>
</Button>
