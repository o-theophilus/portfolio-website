<script>
	import { page } from '$app/state';
	import { Content } from '$lib/layout';
	import { Meta, Icon } from '$lib/macro';
	import { Button } from '$lib/button';

	let error = page.error.message;
	export const data = '';
	export const form = '';
</script>

<Meta title={error} description={error.message} />

<Content>
	<br />
	<br />
	<section>
		<div>
			<strong class="ititle">{page.status}</strong>
			<br />
			{error}
		</div>
		<img src="/error.png" alt="error" />

		<Button href="/">
			<Icon icon="home" />
			Back to Home
		</Button>
	</section>
</Content>
<br />
<br />

<style>
	section {
		display: flex;
		flex-direction: column;
		gap: var(--sp3);
	}
</style>
