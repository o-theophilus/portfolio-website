<script>
	import { api_url, module, _tick, _user } from '$lib/store.js';

	import Content from '$lib/comp/content.svelte';
	import Marked from '$lib/comp/marked.svelte';
	import Meta from '$lib/comp/meta.svelte';
	import Button from '$lib/comp/button.svelte';
	import Tags from '$lib/comp/tags.svelte';

	import Delete from './module/delete_post.svelte';
	import Title from './module/edit_title.svelte';
	import Description from './module/edit_description.svelte';
	import Edit_Tags from './module/edit_tags.svelte';
	import Edit_Content from './module/edit_content.svelte';
	import Edit_Date from './module/edit_date.svelte';
	import Edit_Status from './module/edit_status.svelte';
	import Manage_Photo from './module/manage_photo.svelte';
	import Manage_Video from './module/manage_video.svelte';

	import Comment from './comment_area.svelte';

	export let data;
	let { post } = data;
	let { tags } = data;

	$: if ($_tick) {
		post = $_tick;
		$_tick = '';
	}

	let content = post.content;
	$: {
		content = post.content;
		post.photo_count = 1;
		let is_available = content.search(/{#photo}/) >= 0;
		while (is_available) {
			let photo = `![${post.title}](${api_url}/${post.photos[post.photo_count]})`;
			content = content.replace(/{#photo}/, photo);
			is_available = content.search(/{#photo}/) >= 0;
			post.photo_count = post.photo_count + 1;
		}
	}

	$: {
		post.video_count = 0;
		let is_available = content.search(/{#video}/) >= 0;
		while (is_available) {
			let v = `<iframe 
					width="100%" 
					height="500px"
					frameborder="0" 
					src="https://www.youtube.com/embed/${post.videos[post.video_count]}">
				</iframe>
				`;
			content = content.replace(/{#video}/, v);
			is_available = content.search(/{#video}/) >= 0;
			post.video_count = post.video_count + 1;
		}
	}

	let edit_mode = false;
</script>

<Meta title={post.title} description={post.description} image={post.photos[0]} />

<Content>
	{#if $_user.roles.includes('admin')}
		<Button
			class="tiny"
			on:click={() => {
				edit_mode = !edit_mode;
			}}>Edit Mode: {edit_mode}</Button
		>
		<br />
		<br />
	{/if}
	<img
		src="{api_url}/{post.photos[0] || ''}"
		alt={post.title}
		onerror="this.src='/site/no_photo.png'"
	/>

	{#if $_user.roles.includes('admin') && edit_mode}
		<div class="row">
			<Button
				class="tiny"
				on:click={() => {
					$module = {
						module: Manage_Photo,

						post
					};
				}}>Manage Photo</Button
			>
			{#if post.video_count > 0}
				<Button
					class="tiny"
					on:click={() => {
						$module = {
							module: Manage_Video,
							post
						};
					}}>Manage Video</Button
				>
			{/if}
		</div>
	{/if}

	<br />
	<strong class="big">{post.title}</strong>
	{#if $_user.roles.includes('admin') && edit_mode}
		<Button
			icon="edit"
			class="tiny"
			on:click={() => {
				$module = {
					module: Title,
					post
				};
			}}
		/>
	{/if}

	<br />
	<span class="date">{post.created_at.split('T')[0]}</span>
	{#if $_user.roles.includes('admin') && edit_mode}
		<Button
			icon="edit"
			class="tiny"
			on:click={() => {
				$module = {
					module: Edit_Date,
					post
				};
			}}
		/>
	{/if}

	{#if $_user.roles.includes('admin') && edit_mode}
		<br /><br />
		{post.description}

		<Button
			icon="edit"
			class="tiny"
			on:click={() => {
				$module = {
					module: Description,
					post
				};
			}}
		/>
	{/if}

	<br /><br />
	{#if $_user.roles.includes('admin') && edit_mode}
		<Button
			icon="edit"
			class="tiny"
			on:click={() => {
				$module = {
					module: Edit_Content,
					post
				};
			}}
		/>
	{/if}
	<Marked md={content} />

	<br />

	{#if $_user.roles.includes('admin') && edit_mode}
		<Button
			icon="edit"
			class="tiny"
			on:click={() => {
				$module = {
					module: Edit_Tags,
					post,
					tags_in: tags
				};
			}}
		/>
	{/if}
	<Tags tags={post.tags} />

	{#if $_user.roles.includes('admin') && edit_mode}
		<br /> <br />
		Status: <strong> {post.status}</strong>
		<div class="row">
			<Button
				on:click={() => {
					$module = {
						module: Edit_Status,
						post
					};
				}}>Edit Status</Button
			>
			<Button
				on:click={() => {
					$module = {
						module: Delete,
						post
					};
				}}>Delete</Button
			>
		</div>
	{/if}
	<br /><br />
</Content>

<Comment {post} />
<br />
<br />

<style>
	.big {
		font-size: x-large;
		color: var(--accent1);
	}
	img {
		background-color: var(--accent4);
	}
</style>
