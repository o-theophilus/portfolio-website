<script>
	import { page } from '$app/state';
	import { Content } from '$lib/layout';
	import { Meta } from '$lib/macro';
	import { Button } from '$lib/button';

	let error = page.error.message;
	console.log(page);
</script>

<Meta title={error} />

<Content>
	<div class="page_title">{page.status}</div>
	{error}
	<br />
	<br />
	<br />
	<img src="/error.png" alt="error" />
	<br />
	<br />
	<br />

	<Button icon="house" href="/">Back to Home</Button>
</Content>

<style>
	img {
		width: 100%;
	}
</style>
