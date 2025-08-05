<script>
	import { Button } from '.';

	let { children, ...props } = $props();
</script>

<Button
	{...props}
	--button-height="24px"
	--button-border-radius="20px"
	--button-font-size="0.8rem"
	outline
>
	{@render children()}
</Button>
