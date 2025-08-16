<script>
	import { page } from '$app/state';
	import { module, app } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { Icon } from '$lib/macro';
	import { Form, Row, Br } from '$lib/layout';

	let text = `Check Out: ${module.value.title}`;

	let platforms = [
		{
			name: 'facebook',
			href: `https://www.facebook.com/sharer.php?u=${page.url.href}`
		},
		{
			name: 'twitter',
			href: `http://twitter.com/share?text=${text}&url=${page.url.href}&hashtags=portfolio,website`
		},
		{
			name: 'whatsapp',
			href: `whatsapp://send?text=${text}%20${page.url.href}`
		},
		{
			name: 'telegram',
			href: `https://telegram.me/share/url?url=${page.url.href}&text=${text}`
		}
	];

	const click = (on) => {
		fetch(`${import.meta.env.VITE_BACKEND}/log`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify({
				action: 'shared',
				entity_type: 'post',
				entity_key: module.post.key,
				misc: { on }
			})
		});
	};
</script>

<Form title="Share">
	<Br />
	<Row>
		{#each platforms as x}
			<Button
				target="_blank"
				title={x.name}
				onclick={() => {
					click(x.name);
				}}
				href={x.href}
			>
				<Icon icon={x.name} size="1.4" />
			</Button>
		{/each}
	</Row>
</Form>
